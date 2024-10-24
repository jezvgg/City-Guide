namespace uTraverse.AiAPI.Services;


/// <summary>
/// Manages resolution of XIDs by indexes
/// </summary>
public interface IPlaceResolverService
{
    /// <summary>
    /// Resolves XID from index
    /// </summary>
    /// <param name="index">Index to look for</param>
    /// <returns>XID of the place</returns>
    public Task<string> GetXidForIndexAsync(long index);

    /// <summary>
    /// Resolves multiple XIDs from indexes
    /// </summary>
    /// <param name="indexes">Collection of indexes to look for</param>
    /// <returns>Collection of XIDs</returns>
    public Task<IEnumerable<string>> GetXidsForIndexesAsync(IEnumerable<long> indexes, string city);
}
