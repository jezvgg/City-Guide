using BenchmarkDotNet.Attributes;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using uTraverse.PlacesAPI.Data;
using uTraverse.PlacesAPI.Models;

namespace uTraverse.Benchmarks.Data;

/* Conclusion:
 * JOIN operations perform a bit slower than IN operations;
 * 
 * Arrays perform ever so slighthly slower than IEnumerable as method parameters.
 * 0.05 ms difference for 1000 items and ~5% difference in performance shall be considered insignificant, thereby usage of IEnumerable as a method parameter is justfied
 */

public class DatabaseBenchmark
{
    public PlacesDbContext db;
    public List<Place> Places;
    public List<Guid> MasterIdList;
    public List<Guid> IdList;
    public Guid[] IdArray;
    public IEnumerable<Guid> IdEnumerable;

    public const int ItemCount = 1000;

    [Params(10, 100, 1000)]
    public int GetCount;

    [GlobalSetup]
    public void Setup()
    {
        var builder = Host.CreateApplicationBuilder();
        builder.Services.AddDbContext<PlacesDbContext>(conf =>
        {
            conf.UseNpgsql("User ID=test;Password=test;Host=localhost;Port=5434;");
        });

        var app = builder.Build();

        db = app.Services.GetRequiredService<PlacesDbContext>();

        MasterIdList = [];
        Places = [];

        for (int i = 0; i < ItemCount; i++)
        {
            var place = new Place() { Address = "", Name = "" };
            Places.Add(place);
            MasterIdList.Add(place.Id);
            db.Places.Add(place);
        }

        db.SaveChanges();
    }

    [GlobalCleanup]
    public void Cleanup()
    {
        db.RemoveRange(Places);
        db.SaveChanges();
        db.Dispose();
    }

    [IterationSetup]
    public void IterationSetup()
    {
        List<Guid> left = [.. MasterIdList];
        List<Guid> aggreg = [];
        for (int i = 0; i < GetCount; i++)
        {
            var id = Random.Shared.Next(left.Count);
            var guid = left[id];
            left.Remove(guid);
            aggreg.Add(guid);
        }

        IdList = aggreg;
        IdArray = [.. aggreg];
        IdEnumerable = [.. aggreg];
    }

    [Benchmark(Baseline = true)]
    public List<Place> GetPlacesContainsArray()
    {
        return [.. db.Places.Where(x => IdArray.Contains(x.Id))];
    }

    [Benchmark]
    public List<Place> GetPlacesContainsEnumerable()
    {
        return [.. db.Places.Where(x => IdEnumerable.Contains(x.Id))];
    }

    [Benchmark]
    public List<Place> GetPlacesJoinArray()
    {
        return [.. db.Places.Join(IdArray, e => e.Id, id => id, (e, id) => e)];
    }

}
