﻿using uTraverse.AiAPI.Exceptions;

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
    Task<IEnumerable<long>> GetPlaceIndexesAsync(string prompt, string city);  // The usage of IEnumerable as a return type here is justified by benchmarks, showing negligible performance **benefits** from using IEnumerable
    Task<IEnumerable<long>> GetPlaceIndexesAsync(IFormFile imgPrompt, string city);
}