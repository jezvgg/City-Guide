using uTraverse.AiAPI.Exceptions;

namespace uTraverse.AiAPI.Services;

/// <summary>
/// Manages communication with the AI microservice
/// </summary>
/// <param name="logger">A logger instance for internal usage</param>
/// <param name="httpClient">An HttpClient instance for communication with the AI microservice (should have BaseAddress set to the AI microservice URL)</param>
public class AiService(ILogger<AiService> logger, HttpClient httpClient) : IAiService
{
    private readonly ILogger _logger = logger;

    public async Task<IEnumerable<long>> GetPlaceIndexesAsync(string prompt, string city)
    {
        // TODO: Add distributed caching to offload the AI and speed up execution

        _logger.LogDebug("Retrieving place IDs from the Prompt: {Prompt}", prompt);

        // Retrieve the IDs for the Prompt (TODO: replace with a better endpoint URL)
        var multipart = new MultipartFormDataContent();

        multipart.Add(new StringContent(prompt), "prompt");

        var response = await httpClient.PostAsync($"/get_by_prompt/{city}", multipart);

        // Throw an exception if received null
        if (response is null)
        {
            _logger.LogWarning("AI API returned a null response");
            throw new ApiResponseNullException("AI API returned a null response");
        }

        var res = await response.Content.ReadFromJsonAsync<IEnumerable<long>>();

        // Throw an exception if received null
        if (res is null)
        {
            _logger.LogWarning("Deserialize response is null");
            throw new ApiResponseNullException("Deserialize response is null");
        }

        _logger.LogDebug("AI API request was successful");

        return res;
    }

    public async Task<IEnumerable<long>> GetPlaceIndexesAsync(IFormFile imgPrompt, string city)
    {
        // TODO: Add distributed caching to offload the AI and speed up execution

        var stream = imgPrompt.OpenReadStream();

        // Retrieve the IDs for the Prompt (TODO: replace with a better endpoint URL)
        var response = await httpClient.PostAsync($"/get_by_image/{city}", new StreamContent(stream));
        //GetFromJsonAsync<IEnumerable<Guid>>($"/?Prompt={imgPrompt}");

        // Throw an exception if received null
        if (response is null)
        {
            _logger.LogWarning("AI API returned a null response");
            throw new ApiResponseNullException("AI API returned a null response");
        }

        var res = await response.Content.ReadFromJsonAsync<IEnumerable<long>>();

        // Throw an exception if received null
        if (res is null)
        {
            _logger.LogWarning("Deserialize response is null");
            throw new ApiResponseNullException("Deserialize response is null");
        }

        _logger.LogDebug("AI API request was successful");

        return res;
    }
}
