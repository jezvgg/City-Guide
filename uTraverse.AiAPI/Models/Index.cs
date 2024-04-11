using System.ComponentModel.DataAnnotations;

namespace uTraverse.AiAPI.Models;


public class Index
{
    public long Id { get; set; }

    [Length(1, 16)]
    public required string XID { get; set; }
}