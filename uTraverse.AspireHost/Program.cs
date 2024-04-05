// Create the application builder
var builder = DistributedApplication.CreateBuilder(args);

// Add the API project dependency
builder.AddProject<Projects.uTraverse_PlacesAPI>("utraverse-placesapi");

// Run the app (Aspire AppHost)
builder.Build().Run();