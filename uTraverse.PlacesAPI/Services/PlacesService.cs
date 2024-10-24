using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Distributed;
using System.Text.Json;
using uTraverse.PlacesAPI.Data;
using uTraverse.PlacesAPI.Exceptions;
using uTraverse.PlacesAPI.Models;

namespace uTraverse.PlacesAPI.Services;

/// <summary>
/// Handles retrieving places details from the DB
/// </summary>
/// <param name="logger">Logger for internal usage</param>
/// <param name="db">DbContext for querying</param>
public class PlacesService(ILogger<PlacesService> logger, PlacesDbContext db, IDistributedCache cache) : IPlacesService
{
    private readonly ILogger _logger = logger;

    public async Task<Place> GetPlaceByIdCacheAsync(string xid)
    {
        var placeString = await cache.GetStringAsync(xid);

        Place? place;

        if (placeString is null)
        {
            _logger.LogDebug("Retrieving place with ID from DB: {xid}", xid);

            place = await db.Places.FirstOrDefaultAsync(x => x.XID == xid);

            placeString = JsonSerializer.Serialize(place);
            await cache.SetStringAsync(xid, placeString, new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1)
            });
        }
        else
        {
            _logger.LogDebug("Retrieving place with ID from cache: {xid}", xid);
            place = JsonSerializer.Deserialize<Place>(placeString);
        }

        // Throw an exception if the place is not found
        if (place is not null) return place;

        _logger.LogWarning("Couldn't find place with ID: {xid}", xid);
        throw new PlaceNotFoundException($"No place with such ID: {xid}");
    }

    private async Task<Place> GetPlaceByIdAsync(string xid)
    {
        _logger.LogDebug("Retrieving place with ID: {xid}", xid);

        var place = await db.Places.FirstOrDefaultAsync(x => x.XID == xid);

        // Throw an exception if the place is not found
        if (place is null)
        {
            _logger.LogWarning("Couldn't find place with ID: {xid}", xid);
            throw new PlaceNotFoundException($"No place with such ID: {xid}");
        }

        _logger.LogDebug("Retrieved place with ID: {xid}", place.XID);

        return place;
    }

    public async Task<IEnumerable<Place>> GetPlacesByIdsAsync(IEnumerable<string> ids)
    {
        Place? place = null;
        List<Place> places = [];

        // Convert to HashSet for better performance
        var idsHash = ids.ToHashSet();
        HashSet<string> dbIds = [];
        string? placeString;

        // Retrieve cached places
        foreach (var id in idsHash)
        {
            placeString = await cache.GetStringAsync(id);
            place = null;
            if (placeString is not null)
            {
                place = JsonSerializer.Deserialize<Place>(placeString);
            }

            if (place is null)
            {
                dbIds.Add(id);
                continue;
            }

            places.Add(place);
        }

        _logger.LogDebug("Retrieving places with IDs: {ids}", dbIds);

        var placesDb = await db.Places.Where(e => dbIds.Contains(e.XID)).ToArrayAsync();

        //// Cache places
        foreach (var placeDb in placesDb)
        {
            placeString = JsonSerializer.Serialize(placeDb);
            await cache.SetStringAsync(placeDb.XID, placeString, new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1)
            });
        }

        // Get all places whose ID are in the list
        places = [.. places, .. placesDb];

        // Throw exception if no places were found
        if (places is null)
        {
            _logger.LogWarning("Couldn't find places with given IDs");
            throw new PlaceNotFoundException($"No places with such IDs were found");
        }

        _logger.LogDebug("Retrieval succeeded");

        return places;
    }
}
