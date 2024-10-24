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
 * Arrays perform ever so slightly slower than IEnumerable as method parameters.
 * 0.05 ms difference for 1000 items and ~5% difference in performance shall be considered insignificant, thereby usage of IEnumerable as a method parameter is justified
 */

public class DatabaseBenchmark
{
    private PlacesDbContext _db;
    private List<Place> _places;
    private List<string> _masterIdList;
    private string[] _idArray;
    private IEnumerable<string> _idEnumerable;

    private const int ItemCount = 1000;

    [Params(10, 100, 1000)] public int _getCount = 10;

    [GlobalSetup]
    public void Setup()
    {
        var builder = Host.CreateApplicationBuilder();
        builder.Services.AddDbContext<PlacesDbContext>(conf =>
        {
            conf.UseNpgsql("User ID=test;Password=test;Host=localhost;Port=5434;");
        });

        var app = builder.Build();

        _db = app.Services.GetRequiredService<PlacesDbContext>();

        _masterIdList = [];
        _places = [];

        for (var i = 0; i < ItemCount; i++)
        {
            var place = new Place
            {
                XID = "null",
                Name = "null",
                Categories = [],
                City = "null",
                WikiId = "null",
                Latitude = 0,
                Longitude = 0
            };
            _places.Add(place);
            _masterIdList.Add(place.XID);
            _db.Places.Add(place);
        }

        _db.SaveChanges();
    }

    [GlobalCleanup]
    public void Cleanup()
    {
        _db.RemoveRange(_places);
        _db.SaveChanges();
        _db.Dispose();
    }

    [IterationSetup]
    public void IterationSetup()
    {
        List<string> left = [.. _masterIdList];
        List<string> aggreg = [];
        for (int i = 0; i < _getCount; i++)
        {
            var id = Random.Shared.Next(left.Count);
            var guid = left[id];
            left.Remove(guid);
            aggreg.Add(guid);
        }

        _idArray = [.. aggreg];
        _idEnumerable = [.. aggreg];
    }

    [Benchmark(Baseline = true)]
    public List<Place> GetPlacesContainsArray()
    {
        return [.. _db.Places.Where(x => _idArray.Contains(x.XID))];
    }

    [Benchmark]
    public List<Place> GetPlacesContainsEnumerable()
    {
        return [.. _db.Places.Where(x => _idEnumerable.Contains(x.XID))];
    }

    [Benchmark]
    public List<Place> GetPlacesJoinArray()
    {
        return [.. _db.Places.Join(_idArray, e => e.XID, id => id, (e, id) => e)];
    }

}
