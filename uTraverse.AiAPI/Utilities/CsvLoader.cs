using CsvHelper;
using System.Globalization;
using uTraverse.AiAPI.Data;
using Index = uTraverse.AiAPI.Models.Index;

namespace uTraverse.PlacesAPI.Utility;


public class CsvLoader(AiDbContext db)
{
    public void LoadFile(string path)
    {
        using var file = new StreamReader(File.OpenRead(path));

        using var csv = new CsvReader(file, CultureInfo.InvariantCulture);

        var records = csv.GetRecords<IndexDto>();

        foreach (var record in records)
        {
            var index = new Index
            {
                XID = record.XID,
                Id = record.Index
            };

            db.Indexes.Add(index);
        }

        db.SaveChanges();
    }

    private class IndexDto
    {
        public string XID { get; set; }
        public int Index { get; set; }
    }
}