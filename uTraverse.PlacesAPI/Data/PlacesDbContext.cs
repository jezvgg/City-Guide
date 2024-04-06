using Microsoft.EntityFrameworkCore;

namespace uTraverse.PlacesAPI.Data;

public class PlacesDbContext : DbContext
{
    public PlacesDbContext(DbContextOptions options) : base(options)
    {
        // Create DB and DB tables if they don't exist
        Database.EnsureCreated();
    }
}
