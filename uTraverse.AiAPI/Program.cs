using uTraverse.AiAPI.Exceptions;
using uTraverse.AiAPI.Services;
using uTraverse.AspireServiceDefaults;

// Create the API builder
var builder = WebApplication.CreateBuilder(args);

// Add default services (logging, configuration, etc.)
builder.AddServiceDefaults();

builder.Services.AddHttpClient<IAiService, AiService>(client => client.BaseAddress = new Uri("http://localhost:5076"));  // For test use only
//builder.Services.AddHttpClient<AIService>(client => client.BaseAddress = new Uri("http://utraverse-placematcher"));

var app = builder.Build();

// Map health-checks and other Aspire stuff
app.MapDefaultEndpoints();

// Map the /places API section
var places = app.MapGroup("/ai/places");

places.MapPost("/text", async (TextPromptRequest request, IAiService ai) =>
{
    app.Logger.LogDebug("Endpoint call on / with Prompt: {Prompt}", request.Prompt);

    try
    {
        // Retrieve place IDs from the AI microservice for the given Prompt
        var res = await ai.GetPlaceIdsAsync(request.Prompt, request.City);

        return Results.Ok(res);
    }
    catch (ApiResponseNullException)
    {
        // The AI microservice has returned null
        return Results.NotFound();
    }
});

places.MapPost("/img", async (ImagePromptRequest request, IAiService ai) =>
{
    try
    {
        // Retrieve place IDs from the AI microservice for the given Prompt
        var res = await ai.GetPlaceIdsAsync(request.Image, request.City);

        return Results.Ok(res);
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