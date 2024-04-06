using uTraverse.AiAPI.Exceptions;
using uTraverse.AiAPI.Services;

// Create the API builder
var builder = WebApplication.CreateBuilder(args);

// Add default services (logging, configuration, etc.)
builder.AddServiceDefaults();

builder.Services.AddHttpClient<AIService>(client => client.BaseAddress = new Uri("http://localhost:5076"));  // For test use only
//builder.Services.AddHttpClient<AIService>(client => client.BaseAddress = new Uri("http://utraverse-placematcher"));

var app = builder.Build();

// Map healthchecks and other Aspire stuff
app.MapDefaultEndpoints();

// Map the /places API section
var places = app.MapGroup("/places");

places.MapGet("/match/text", async (string prompt, AIService ai) =>
{
    app.Logger.LogDebug("Endpoint call on / with prompt: {prompt}", prompt);

    try
    {
        // Retrieve place IDs from the AI microservice for the given prompt
        var res = await ai.GetPlaceIdsAsync(prompt);

        return Results.Ok(res);
    }
    catch (ApiResponseNullException)
    {
        // The AI microservice has returned null
        return Results.NotFound();
    }
});

app.Run();