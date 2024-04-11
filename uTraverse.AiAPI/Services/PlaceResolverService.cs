using Microsoft.EntityFrameworkCore;
using uTraverse.AiAPI.Data;
using uTraverse.AiAPI.Exceptions;

namespace uTraverse.AiAPI.Services;


/// <summary>
/// Manages resolution of XIDs by their indexes
/// </summary>
/// <param name="db">Database context containing index table</param>
public class PlaceResolverService (AiDbContext db) : IPlaceResolverService
{
    public async Task<string> GetXidForIndexAsync(long index)
    {
        var ind = await db.Indexes.FindAsync(index);

        if (ind is null)
            throw new IndexNotFoundException(nameof(ind));

        return ind.XID;
    }

    public async Task<IEnumerable<string>> GetXidsForIndexesAsync(IEnumerable<long> indexes)
    {
        var inds = await db.Indexes.Where(e => indexes.Contains(e.Id)).Select(e => e.XID).ToArrayAsync();

        return inds;
    }
}
