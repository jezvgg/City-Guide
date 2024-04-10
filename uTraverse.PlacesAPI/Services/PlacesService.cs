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

    public async Task<Place> GetPlaceByIdCacheAsync(Guid id)
    {
        // TODO: Add distributed caching
        var placeString = await cache.GetStringAsync(id.ToString());

        Place? place;

        if (placeString is null)
        {
            _logger.LogDebug("Retrieving place with ID from DB: {id}", id);

            place = await db.Places.FirstOrDefaultAsync(x => x.Id == id);

            placeString = JsonSerializer.Serialize(place);
            await cache.SetStringAsync(id.ToString(), placeString, new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1)
            });
        }
        else
        {
            _logger.LogDebug("Retrieving place with ID from cache: {id}", id);
            place = JsonSerializer.Deserialize<Place>(placeString);
        }

        // Throw an exception if the place is not found
        if (place is not null) return place;

        _logger.LogWarning("Couldn't find place with ID: {id}", id);
        throw new PlaceNotFoundException($"No place with such ID: {id}");
    }

    private async Task<Place> GetPlaceByIdAsync(Guid id)
    {
        // TODO: Add distributed caching

        _logger.LogDebug("Retrieving place with ID: {id}", id);

        var place = await db.Places.FirstOrDefaultAsync(x => x.Id == id);

        // Throw an exception if the place is not found
        if (place is null)
        {
            _logger.LogWarning("Couldn't find place with ID: {id}", id);
            throw new PlaceNotFoundException($"No place with such ID: {id}");
        }

        _logger.LogDebug("Retrieved place with ID: {id}", place.Id);

        return place;
    }

    public async Task<IEnumerable<Place>> GetPlacesByIdsAsync(IEnumerable<Guid> ids)
    {
        Place? place = null;
        List<Place> places = [];
        // TODO: Add distributed caching

        // Convert to HashSet for better performance
        var idsHash = ids.ToHashSet();
        HashSet<Guid> bdIds = [];
        string? placeString;

        // Short-circuit if length is < 2
        switch (idsHash.Count)
        {
            // Return empty if no IDs were passed
            case 0:
                return [];
            // Return the only element
            case 1:
                {
                    place = await GetPlaceByIdCacheAsync(idsHash.First());

                    return [place];
                }
        }

        foreach (var id in idsHash)
        {
            placeString = await cache.GetStringAsync(id.ToString());
            if (placeString is not null)
            {
                place = JsonSerializer.Deserialize<Place>(placeString);
            }

            if (place is null)
            {
                bdIds.Add(id);
                continue;
            }

            places.Add(place);
        }

        switch (bdIds.Count)
        {
            // Return empty if no IDs were passed
            case 0:
                return places;
            // Return the only element
            case 1:
                {
                    place = await GetPlaceByIdAsync(bdIds.First());

                    return [.. places, place];
                }
        }

        _logger.LogDebug("Retrieving places with IDs: {ids}", bdIds);

        var placesDb = await db.Places.Where(e => bdIds.Contains(e.Id)).ToArrayAsync();

        foreach (var placeDb in placesDb)
        {
            placeString = JsonSerializer.Serialize(placeDb);
            await cache.SetStringAsync(placeDb.Id.ToString(), placeString, new DistributedCacheEntryOptions
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
