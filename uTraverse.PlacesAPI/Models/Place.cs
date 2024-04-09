using System.ComponentModel.DataAnnotations;

namespace uTraverse.PlacesAPI.Models;

public class Place
{
    public Guid Id { get; set; } = Guid.NewGuid();

    [MaxLength(128)]
    public required string Name { get; set; }

    [MaxLength(512)]
    public string? Description { get; set; }

    [MaxLength(128)]
    public required string Address { get; set; }

    public decimal Latitude { get; set; }

    public decimal Longitude { get; set; }
}
