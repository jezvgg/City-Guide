using Microsoft.EntityFrameworkCore;
using uTraverse.PlacesAPI.Data;
using uTraverse.PlacesAPI.Exceptions;
using uTraverse.PlacesAPI.Models;

namespace uTraverse.PlacesAPI.Services;

/// <summary>
/// Handles retrieving places details from the DB
/// </summary>
/// <param name="logger">Logger for internal usage</param>
/// <param name="db">DbContext for querying</param>
public class PlacesService(ILogger<PlacesService> logger, PlacesDbContext db) : IPlacesService
{
    private readonly ILogger _logger = logger;

    public async Task<Place> GetPlaceByIdAsync(Guid id)
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
        // TODO: Add distributed caching

        // Convert to HashSet for better performance
        var idsHash = ids.ToHashSet();

        // Short-circuit if length is < 2
        switch (idsHash.Count)
        {
            // Return empty if no IDs were passed
            case 0:
                return [];
            // Return the only element
            case 1:
            {
                var place = await GetPlaceByIdAsync(idsHash.First());

                return [place];
            }
        }

        _logger.LogDebug("Retrieving places with IDs: {ids}", idsHash);

        // Get all places whose ID are in the list
        var places = db.Places.Where(e => idsHash.Contains(e.Id));

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
