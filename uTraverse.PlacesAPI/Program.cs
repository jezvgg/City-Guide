using uTraverse.PlacesAPI.Data;
using uTraverse.PlacesAPI.Exceptions;
using uTraverse.PlacesAPI.Services;

// Create the API builder
var builder = WebApplication.CreateBuilder(args);

// Add default services (logging, configuration, etc.)
builder.AddServiceDefaults();

// Add PostgreSQL Places DB context
builder.AddNpgsqlDbContext<PlacesDbContext>("utraverse-placesdb");

// Add a service to interact with the Places DB
builder.Services.AddScoped<IPlacesService, PlacesService>();

var app = builder.Build();

// Map healthchecks and other Aspire stuff
app.MapDefaultEndpoints();

// Map /places section of the API
var places = app.MapGroup("/places");

places.MapGet("/", async (Guid[] ids, IPlacesService placesService) =>
{
    app.Logger.LogDebug("Hit /places/batch/ids endpoint for IDs: {ids}", ids);

    try
    {
        var places = await placesService.GetPlacesByIdsAsync(ids);

        return Results.Ok(places);
    }
    catch (PlaceNotFoundException)
    {
        // The places with such IDs could not be found
        return Results.NotFound();
    }
});

app.Run();