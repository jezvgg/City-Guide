using BenchmarkDotNet.Running;
using uTraverse.Benchmarks.Data;
using uTraverse.Benchmarks.Web;

BenchmarkRunner.Run<DatabaseBenchmark>();
BenchmarkRunner.Run<JsonBenchmarks>();