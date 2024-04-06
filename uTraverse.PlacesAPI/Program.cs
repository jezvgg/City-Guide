// Create the API builder
using uTraverse.PlacesAPI.Data;

var builder = WebApplication.CreateBuilder(args);

// Add default services (logging, configuration, etc.)
builder.AddServiceDefaults();

builder.AddNpgsqlDbContext<PlacesDbContext>("utraverse-placesdb");

var app = builder.Build();

// Map healthchecks and other Aspire stuff
app.MapDefaultEndpoints();

app.Run();