using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace uTraverse.PlacesAPI.Models;

public class Place
{

    [Key] public required string XID { get; set; }

    [Length(1, 128)]
    public required string Name { get; set; }

    [Length(0, 256)]
    public string? Description { get; set; }

    public required IEnumerable<string> Categories { get; set; }

    [Length(1, 64)]
    public required string City { get; set; }

    [Length(1, 10)]
    public required string WikiId { get; set; }

    public decimal Latitude { get; set; }

    public decimal Longitude { get; set; }
}
