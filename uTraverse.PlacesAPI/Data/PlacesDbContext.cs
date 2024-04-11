using Microsoft.EntityFrameworkCore;
using uTraverse.PlacesAPI.Models;

namespace uTraverse.PlacesAPI.Data;

public sealed class PlacesDbContext : DbContext
{
    public DbSet<Place> Places { get; set; }

    public PlacesDbContext(DbContextOptions options) : base(options)
    {
        // Create DB and DB tables if they don't exist
        Database.EnsureCreated();
    }
}
