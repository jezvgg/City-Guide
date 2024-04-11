using Microsoft.AspNetCore.Mvc;
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

builder.Services.AddCors(policy =>
{
    policy.AddDefaultPolicy(p => p.AllowAnyHeader().AllowAnyMethod().AllowAnyOrigin());
});

builder.Services.AddAntiforgery();

//builder.Services.AddHttpClient<IAiService, AiService>(client => client.BaseAddress = new Uri("http://localhost:5076"));  // For test use only
builder.Services.AddHttpClient<IAiService, AiService>(client => client.BaseAddress = new Uri("http://172.17.54.27:5000"));

builder.Services.AddScoped<IPlaceResolverService, PlaceResolverService>();

var app = builder.Build();

app.UseAntiforgery();
app.UseCors();

// Map health-checks and other Aspire stuff
app.MapDefaultEndpoints();

// Map the /places API section
var places = app.MapGroup("/ai/places");

places.MapPost("/text", async ([FromForm] TextPromptRequest request, IAiService ai, IPlaceResolverService placeResolver) =>
{
    app.Logger.LogDebug("Endpoint call on / with Prompt: {Prompt}", request.Prompt);

    try
    {
        // Retrieve place IDs from the AI microservice for the given Prompt
        var res = await ai.GetPlaceIndexesAsync(request.Prompt, request.City);

        var xids = await placeResolver.GetXidsForIndexesAsync(res);

        return Results.Ok(xids.Take(10));
    }
    catch (ApiResponseNullException)
    {
        // The AI microservice has returned null
        return Results.NotFound();
    }
}).DisableAntiforgery();

places.MapPost("/img", async ([FromForm] ImagePromptRequest request, IAiService ai, IPlaceResolverService placeResolver) =>
{
    try
    {
        // Retrieve place IDs from the AI microservice for the given Prompt
        var res = await ai.GetPlaceIndexesAsync(request.Image, request.City);

        var xids = await placeResolver.GetXidsForIndexesAsync(res);

        return Results.Ok(xids.Take(10));
    }
    catch (ApiResponseNullException)
    {
        // The AI microservice has returned null
        return Results.NotFound();
    }
}).DisableAntiforgery();

app.Run();

record ImagePromptRequest(IFormFile Image, string City);
record TextPromptRequest(string Prompt, string City);