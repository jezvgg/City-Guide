using System.Text.Json.Serialization;

namespace uTraverse.AiAPI.Utility;

/// <summary>
/// Provides support for JSON (de)serialization. Serialized/deserialized types shall be registered here
/// </summary>
[JsonSerializable(typeof(Guid[]))]
internal partial class AppJsonSerializerContext : JsonSerializerContext
{

}