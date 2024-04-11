using uTraverse.AiAPI.Data;
using uTraverse.AiAPI.Exceptions;
using uTraverse.AiAPI.Services;
using uTraverse.AspireServiceDefaults;

// Create the API builder
var builder = WebApplication.CreateBuilder(args);

// Add default services (logging, configuration, etc.)
builder.AddServiceDefaults();

// Add indexes DB reference
builder.AddNpgsqlDbContext<AiDbContext>("utraverse-indexdb");

builder.Services.AddHttpClient<IAiService, AiService>(client => client.BaseAddress = new Uri("http://localhost:5076"));  // For test use only
//builder.Services.AddHttpClient<AIService>(client => client.BaseAddress = new Uri("http://utraverse-placematcher"));

builder.Services.AddScoped<IPlaceResolverService, PlaceResolverService>();

var app = builder.Build();

// Map health-checks and other Aspire stuff
app.MapDefaultEndpoints();

// Map the /places API section
var places = app.MapGroup("/ai/places");

places.MapPost("/text", async (TextPromptRequest request, IAiService ai, IPlaceResolverService placeResolver) =>
{
    app.Logger.LogDebug("Endpoint call on / with Prompt: {Prompt}", request.Prompt);

    try
    {
        // Retrieve place IDs from the AI microservice for the given Prompt
        var res = await ai.GetPlaceIndexesAsync(request.Prompt, request.City);

        var xids = placeResolver.GetXidsForIndexesAsync(res);

        return Results.Ok(xids);
    }
    catch (ApiResponseNullException)
    {
        // The AI microservice has returned null
        return Results.NotFound();
    }
});

places.MapPost("/img", async (ImagePromptRequest request, IAiService ai, IPlaceResolverService placeResolver) =>
{
    try
    {
        // Retrieve place IDs from the AI microservice for the given Prompt
        var res = await ai.GetPlaceIndexesAsync(request.Image, request.City);

        var xids = placeResolver.GetXidsForIndexesAsync(res);

        return Results.Ok(xids);
    }
    catch (ApiResponseNullException)
    {
        // The AI microservice has returned null
        return Results.NotFound();
    }
});

app.Run();

record ImagePromptRequest(IFormFile Image, string City);
record TextPromptRequest(string Prompt, string City);