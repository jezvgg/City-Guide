// Create the application builder
var builder = DistributedApplication.CreateBuilder(args);

// Add the Places API project reference
builder.AddProject<Projects.uTraverse_PlacesAPI>("utraverse-placesapi");

// Add the AI API project reference
builder.AddProject<Projects.uTraverse_AiAPI>("utraverse-aiapi");

// Run the app (Aspire AppHost)
builder.Build().Run();