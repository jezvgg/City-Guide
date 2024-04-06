namespace uTraverse.AiAPI.Services;

/// <summary>
/// Manages communication with the AI microservice
/// </summary>
public interface IAIService
{
    /// <summary>
    /// Retrieves an array of place IDs matching the given prompt
    /// </summary>
    /// <param name="prompt">The prompt to match the places</param>
    /// <returns>An array of place IDs that match the prompt</returns>
    Task<Guid[]> GetPlaceIdsAsync (string prompt);
}