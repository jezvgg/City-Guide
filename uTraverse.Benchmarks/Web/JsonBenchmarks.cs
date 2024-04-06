using BenchmarkDotNet.Attributes;
using System.Text.Json;
using uTraverse.PlacesAPI.Models;

namespace uTraverse.Benchmarks.Web;

/* Conslusion:
 * IEnumerable performed 0.04% better than array and 0.06% better than list.
 * This shall be considered an insignificant (more so, positive) performance difference.
 * Usage of IEnumerable as a return type to be passed to the serializer is thereby justified.
 */
public class JsonBenchmarks
{
    public Place[] PlaceArray;
    public List<Place> PlaceList;
    public IEnumerable<Place> PlaceIEnumerable;

    [Params(10000)]
    public int ItemNumber;

    [GlobalSetup]
    public void Setup()
    {
        List<Place> places = [];
        for (int i = 0; i < ItemNumber; i++)
        {
            places.Add(new() { Address = "", Name = "" });
        }

        PlaceList = [.. places];
        PlaceArray = [.. places];
        PlaceIEnumerable = [.. places];
    }

    [Benchmark]
    public string SerializeArrayAsync()
    {
        return JsonSerializer.Serialize(PlaceArray);
    }

    [Benchmark]
    public string SerializeListAsync()
    {
        return JsonSerializer.Serialize(PlaceList);
    }

    [Benchmark]
    public string SerializeIEnumerableAsync()
    {
        return JsonSerializer.Serialize(PlaceIEnumerable);
    }
}
