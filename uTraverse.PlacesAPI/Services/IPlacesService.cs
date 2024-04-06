using uTraverse.PlacesAPI.Models;

namespace uTraverse.PlacesAPI.Services
{
    /// <summary>
    /// Handles retrieving place details from the DB
    /// </summary>
    public interface IPlacesService
    {
        /// <summary>
        /// Get place details by place ID
        /// </summary>
        /// <param name="id">The ID of the place</param>
        /// <returns>Place instance containing the details of the place with given ID</returns>
        Task<Place> GetPlaceByIdAsync(Guid id);

        /// <summary>
        /// Get details for places with given IDs
        /// </summary>
        /// <param name="ids">A collection of </param>
        /// <returns></returns>
        Task<IEnumerable<Place>> GetPlacesByIdsAsync(IEnumerable<Guid> ids);
        // The usage of IEnumerable as both return type an parameter type here is justified by benchmarks, showing 5% performance decrease (50us @ 1000 entities) which shall be considered negligible
    }
}