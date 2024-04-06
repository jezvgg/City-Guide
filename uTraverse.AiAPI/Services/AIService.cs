using uTraverse.AiAPI.Exceptions;

namespace uTraverse.AiAPI.Services;

/// <summary>
/// Manages communication with the AI microservice
/// </summary>
/// <param name="logger">A logger instance for internal usage</param>
/// <param name="httpClient">An HttpClient instance for communication with the AI microservice (should have BaseAddress set to the AI microservice URL)</param>
public class AIService (ILogger<AIService> logger, HttpClient httpClient) : IAIService
{
    private readonly ILogger _logger = logger;
    private readonly HttpClient _httpClient = httpClient;

    public async Task<Guid[]> GetPlaceIdsAsync (string prompt)
    {
        // TODO: Add distributed caching to offload the AI and speed up execution

        _logger.LogDebug("Retrieving place IDs from the prompt: {prompt}", prompt);

        // Retrieve the IDs for the prompt (TODO: replace with a better endpoint URL)
        var res = await _httpClient.GetFromJsonAsync<Guid[]>($"/?prompt={prompt}");

        // Throw an exception if received null
        if (res is null)
        {
            _logger.LogWarning("AI API returned a null response");
            throw new ApiResponseNullException("AI API returned a null response");
        }

        _logger.LogDebug("AI API request was successful. Retrieved {count} items", res.Length);

        return res;
    }
}
