// Create the application builder
var builder = DistributedApplication.CreateBuilder(args);

// Add PostgresSQL DB container for place details
var placesDb = builder.AddPostgres("utraverse-placesdb");

// Add PostgresSQL DB container for indexes
var indexDb = builder.AddPostgres("utraverse-indexdb");

// Add Redis cache for places
var placesCache = builder.AddRedis("utraverse-placescache");

// Add Redis cache for indexes
var indexCache = builder.AddRedis("utraverse-indexcache");

// Add the place matcher AI container
var placeMatcher = builder.AddContainer("utraverse-placematcher", "utraverse/placematcher").WithEndpoint(5000, 1234);

// Add the Places API project reference
var placesApi = builder.AddProject<Projects.uTraverse_PlacesAPI>("utraverse-placesapi")
    .WithReference(placesDb)
    .WithReference(placesCache);

// Add the AI API project reference
var aiApi = builder.AddProject<Projects.uTraverse_AiAPI>("utraverse-aiapi")
    .WithReference(indexDb)
    .WithReference(indexCache);

// Run the app (Aspire AppHost)
builder.Build().Run();