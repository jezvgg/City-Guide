using Microsoft.EntityFrameworkCore;

namespace uTraverse.AiAPI.Data;


public sealed class AiDbContext : DbContext
{
    public required DbSet<Models.Index> Indexes { get; set; }

    public AiDbContext(DbContextOptions options) : base(options)
    {
        // Ensure the DB is instantiated before accessing it.
        Database.EnsureCreated();
    }
}
