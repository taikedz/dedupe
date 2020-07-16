# Directory Walk Event Handlers

A loadable handler must be defined as a module that provides one function, `process(target_item)`

The sole argument `target_item` is a `WalkerItem`

If the handler wishes to indicate that no further processing should be performed on it, the handler can raise `ddexceptions.ProcessorSkipException`

The handler may return a string to indicate what it has done, which is logged as an `INFO` level message.
