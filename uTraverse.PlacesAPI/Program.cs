// Create the API builder
var builder = WebApplication.CreateBuilder(args);

// Add default services (logging, configuration, etc.)
builder.AddServiceDefaults();

var app = builder.Build();

// Map healthchecks and other Aspire stuff
app.MapDefaultEndpoints();

app.Run();