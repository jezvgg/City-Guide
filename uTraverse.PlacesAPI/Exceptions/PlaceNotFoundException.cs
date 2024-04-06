namespace uTraverse.PlacesAPI.Exceptions;

public class PlaceNotFoundException : Exception
{
    public PlaceNotFoundException() { }

    public PlaceNotFoundException(string message) : base(message) { }

    public PlaceNotFoundException(string message, Exception inner) : base(message, inner) { }
}
