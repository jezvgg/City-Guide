using CsvHelper;
using System.Globalization;
using uTraverse.PlacesAPI.Data;
using uTraverse.PlacesAPI.Models;

namespace uTraverse.PlacesAPI.Utility;


public class CsvLoader (PlacesDbContext db)
{
    public void LoadFile(string path)
    {
        using var file = new StreamReader(File.OpenRead(path));

        using var csv = new CsvReader(file, CultureInfo.InvariantCulture);
        
        var records = csv.GetRecords<PlaceDto>();

        foreach (var record in records)
        {
            var place = new Place
            {
                XID = record.XID,
                Name = record.Name,
                Description = record.Description,
                Categories = record.Categories.ToList(),
                City = record.City,
                WikiId = record.WikiData,
                Latitude = record.Lat,
                Longitude = record.Lon
            };

            if (db.Places.Any(x => x.XID == place.XID)) continue;

            db.Places.Add(place);
        }

        db.SaveChanges();
    }

    private class PlaceDto
    {
        public string XID { get; set; }
        public string Name { get; set; }
        public string Kind { get; set; }
        public IEnumerable<string> Categories => Kind.Split(",");
        public string City { get; set; }
        public string WikiData { get; set; }
        public decimal Lon { get; set; }
        public decimal Lat { get; set; }
        public string Description { get; set; }
    }
}
