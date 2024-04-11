using uTraverse.AspireServiceDefaults;
using uTraverse.PlacesAPI.Data;
using uTraverse.PlacesAPI.Exceptions;
using uTraverse.PlacesAPI.Services;
using uTraverse.PlacesAPI.Utility;

// Create the API builder
var builder = WebApplication.CreateBuilder(args);

// Add default services (logging, configuration, etc.)
builder.AddServiceDefaults();

builder.Services.AddCors(policy =>
{
    policy.AddDefaultPolicy(p => p.AllowAnyHeader().AllowAnyMethod().AllowAnyOrigin());
});

// Add PostgresSQL Places DB context
builder.AddNpgsqlDbContext<PlacesDbContext>("utraverse-placesdb");

//Add Redis Places cache
builder.AddRedisDistributedCache("utraverse-placescache");

// Add a service to interact with the Places DB
builder.Services.AddScoped<IPlacesService, PlacesService>();

var app = builder.Build();

// Map health-checks and other Aspire stuff
app.MapDefaultEndpoints();

app.UseCors();

Thread.Sleep(10000);

using (var scope = app.Services.CreateScope())
{
    var loader = new CsvLoader(scope.ServiceProvider.GetRequiredService<PlacesDbContext>());

    loader.LoadFile("./Datasets/EKB_places (1).csv");
    loader.LoadFile("./Datasets/NN_places.csv");
    loader.LoadFile("./Datasets/Vlaf_places.csv");
    loader.LoadFile("./Datasets/Yar_places.csv");
}

// Map /places section of the API
var places = app.MapGroup("/places");

places.MapGet("/get/batch", async (string[] ids, IPlacesService placesService) =>
{
    app.Logger.LogDebug("Hit /places/batch/ids endpoint");

    try
    {
        var retrievedPlaces = await placesService.GetPlacesByIdsAsync(ids);

        return Results.Ok(retrievedPlaces);
    }
    catch (PlaceNotFoundException)
    {
        // The places with such IDs could not be found
        return Results.NotFound();
    }
}).DisableAntiforgery();

app.Run();