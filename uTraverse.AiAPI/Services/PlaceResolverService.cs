using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Distributed;
using uTraverse.AiAPI.Data;
using uTraverse.AiAPI.Exceptions;

namespace uTraverse.AiAPI.Services;


/// <summary>
/// Manages resolution of XIDs by their indexes
/// </summary>
/// <param name="db">Database context containing index table</param>
public class PlaceResolverService (AiDbContext db, IDistributedCache cache) : IPlaceResolverService
{
    public async Task<string> GetXidForIndexAsync(long index)
    {
        var cached = await cache.GetStringAsync(index.ToString());

        if (cached is { } res) return res;

        var ind = await db.Indexes.FindAsync(index);

        if (ind is null)
            throw new IndexNotFoundException(nameof(ind));

        return ind.XID;
    }

    public async Task<IEnumerable<string>> GetXidsForIndexesAsync(IEnumerable<long> indexes, string city)
    {
        HashSet<string> rest = [];
        var hindexes = indexes.ToArray();

        List<string> res = [];

        foreach (var ind in hindexes)
        {
            var index = city + ind;

            var cached = await cache.GetStringAsync(index.ToString());

            if (cached is { } xcached)
                res.Add(xcached);

            else
                rest.Add(index);
        }

        var dbRes = await db.Indexes.Where(e => rest.Contains(e.Id)).Select(e => e.XID).ToArrayAsync();

        return [.. res, ..dbRes];
    }
}
