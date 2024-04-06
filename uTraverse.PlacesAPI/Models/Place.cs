namespace uTraverse.PlacesAPI.Models;

public class Place
{
    public Guid Id { get; set; } = Guid.NewGuid();

    public required string Name { get; set; }

    public string? Description { get; set; }

    public required string Address { get; set; }

    public float Latitude { get; set; }

    public float Longitude { get; set; }
}
