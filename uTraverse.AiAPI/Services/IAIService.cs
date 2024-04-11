using uTraverse.AiAPI.Exceptions;

namespace uTraverse.AiAPI.Services;

/// <summary>
/// Manages communication with the AI microservice
/// </summary>
public interface IAiService
{
    /// <summary>
    /// Retrieves an array of place IDs matching the given Prompt
    /// </summary>
    /// <param name="prompt">The Prompt to match the places</param>
    /// <returns>An array of place IDs that match the Prompt</returns>
    /// <exception cref="ApiResponseNullException">The AI API returned null response</exception>
    Task<IEnumerable<Guid>> GetPlaceIdsAsync(string prompt);  // The usage of IEnumerable as a return type here is justified by benchmarks, showing negligible performance **benefits** from using IEnumerable
    Task<IEnumerable<Guid>> GetPlaceIdsAsync(IFormFile imgPrompt);
}