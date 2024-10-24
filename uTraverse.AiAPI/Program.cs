using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using uTraverse.AiAPI.Data;
using uTraverse.AiAPI.Exceptions;
using uTraverse.AiAPI.Services;
using uTraverse.PlacesAPI.Utility;



// Create the API builder
var builder = WebApplication.CreateBuilder(args);

// Add default services (logging, configuration, etc.)
builder.AddServiceDefaults();

builder.Services.AddCors(policy =>
{
    policy.AddDefaultPolicy(p => p.AllowAnyHeader().AllowAnyMethod().AllowAnyOrigin());
});

// Add indexes DB reference
//builder.AddNpgsqlDbContext<AiDbContext>("utraverse-indexdb");
builder.Services.AddDbContext<AiDbContext>(build => 
build.UseNpgsql(builder.Configuration.GetConnectionString("Postgres")));

// Add Redis cache for indexes
//builder.AddRedisDistributedCache("utraverse-indexcache");
builder.Services.AddStackExchangeRedisCache(options => 
options.Configuration = builder.Configuration.GetConnectionString("Redis"));

builder.Services.AddAntiforgery();

builder.Services.AddSwaggerGen();
builder.Services.AddEndpointsApiExplorer();

//builder.Services.AddHttpClient<IAiService, AiService>(client => client.BaseAddress = new Uri("http://localhost:5076"));  // For test use only
builder.Services.AddHttpClient<IAiService, AiService>(client => client.BaseAddress = new Uri("http://localhost:1234"));

builder.Services.AddScoped<IPlaceResolverService, PlaceResolverService>();

var app = builder.Build();

app.UseAntiforgery();
app.UseCors();

//if (builder.Environment.IsDevelopment())
//{
    app.UseSwagger();
    app.UseSwaggerUI();
//}

Thread.Sleep(10000);

using (var scope = app.Services.CreateScope())
{
    var loader = new CsvLoader(scope.ServiceProvider.GetRequiredService<AiDbContext>());

    loader.LoadFile("./Datasets/id_to_XID_EKB.csv", "ekb");
    loader.LoadFile("./Datasets/id_to_XID_NN.csv", "nino");
    loader.LoadFile("./Datasets/id_to_XID_Vlad.csv", "vlad");
    loader.LoadFile("./Datasets/id_to_XID_Yaroslavl.csv", "yaros");
}

// Map health-checks and other Aspire stuff
app.MapDefaultEndpoints();

// Map the /places API section
var places = app.MapGroup("/ai/places");

places.MapPost("/test", async (AiDbContext db) =>
{
    db.Indexes.Add(new uTraverse.AiAPI.Models.Index { Id = "1", XID="2" });
    db.SaveChanges();
}).DisableAntiforgery();

places.MapPost("/text", async ([FromForm] TextPromptRequest request, IAiService ai, IPlaceResolverService placeResolver) =>
{
    app.Logger.LogDebug("Endpoint call on / with Prompt: {Prompt}", request.Prompt);

    try
    {
        // Retrieve place IDs from the AI microservice for the given Prompt
        var res = await ai.GetPlaceIndexesAsync(request.Prompt, request.City);

        var xids = await placeResolver.GetXidsForIndexesAsync(res, request.City);

        var w = xids.Distinct().Take(5);

        return Results.Ok(xids.Distinct().Take(5));
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

        var xids = await placeResolver.GetXidsForIndexesAsync(res, request.City);

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