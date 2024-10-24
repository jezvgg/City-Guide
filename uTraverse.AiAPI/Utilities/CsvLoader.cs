using CsvHelper;
using System.Globalization;
using System.Runtime.CompilerServices;
using uTraverse.AiAPI.Data;
using Index = uTraverse.AiAPI.Models.Index;

namespace uTraverse.PlacesAPI.Utility;


public class CsvLoader(AiDbContext db)
{
    public void LoadFile(string path, string city)
    {
        using var file = new StreamReader(File.OpenRead(path));

        using var csv = new CsvReader(file, CultureInfo.InvariantCulture);

        var records = csv.GetRecords<IndexDto>();

        foreach (var record in records)
        {
            var index = new Index
            {
                XID = record.XID,
                Id = city + record.index
            };

            if (db.Indexes.Any(x => x.XID == index.XID)) continue;

            db.Indexes.Add(index);
        }

        db.SaveChanges();
    }

    private class IndexDto
    {
        public int index { get; set; }
        public string XID { get; set; }
    }
}