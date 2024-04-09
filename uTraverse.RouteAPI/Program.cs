using uTraverse.AspireServiceDefaults;

// Create the API builder
var builder = WebApplication.CreateBuilder(args);

// Add default services (logging, configuration, etc.)
builder.AddServiceDefaults();

// Add PostgresSQL Places DB context
//builder.AddNpgsqlDbContext<LocationsDbContext>("utraverse-placesdb");

var app = builder.Build();

// Map health-checks and other Aspire stuff
app.MapDefaultEndpoints();

app.Run();