// Create the API builder (with NativeAOT support)
var builder = WebApplication.CreateSlimBuilder(args);

// Add default services (logging, configuration, etc.)
builder.AddServiceDefaults();

var app = builder.Build();

// Map healthchecks and other Aspire stuff
app.MapDefaultEndpoints();

app.Run();