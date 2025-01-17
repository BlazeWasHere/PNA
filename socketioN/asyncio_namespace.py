import asyncio

from socketioN import namespace


class AsyncNamespace(namespace.Namespace):
    """Base class for asyncio server-side class-based namespaces.

    A class-based namespace is a class that contains all the event handlers
    for a Socket.IO namespace. The event handlers are methods of the class
    with the prefix ``on_``, such as ``on_connect``, ``on_disconnect``,
    ``on_message``, ``on_json``, and so on. These can be regular functions or
    coroutines.

    :param namespace: The Socket.IO namespace to be used with all the event
                      handlers defined in this class. If this argument is
                      omitted, the default namespace is used.
    """

    def is_asyncio_based(self):
        return True

    async def trigger_event(self, event, *args):
        """Dispatch an event to the proper handler method.

        In the most common usage, this method is not overloaded by subclasses,
        as it performs the routing of events to methods. However, this
        method can be overriden if special dispatching rules are needed, or if
        having a single method that catches all events is desired.

        Note: this method is a coroutine.
        """
        handler_name = 'on_' + event
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            if asyncio.iscoroutinefunction(handler) is True:
                try:
                    ret = await handler(*args)
                except asyncio.CancelledError:  # pragma: no cover
                    ret = None
            else:
                ret = handler(*args)
            return ret

    async def emit(self, event, data=None, room=None, skip_sid=None,
                   s_namespace=None, callback=None):
        """Emit a custom event to one or more connected clients.

        The only difference with the :func:`Server.emit` method is
        that when the ``namespace`` argument is not given the namespace
        associated with the class is used.

        Note: this method is a coroutine.
        """
        return await self.server.emit(event, data=data, room=room,
                                      skip_sid=skip_sid,
                                      namespace=s_namespace or self.namespace,
                                      callback=callback)

    async def send(self, data, room=None, skip_sid=None, s_namespace=None,
                   callback=None):
        """Send a message to one or more connected clients.

        The only difference with the :func:`Server.send` method is
        that when the ``namespace`` argument is not given the namespace
        associated with the class is used.

        Note: this method is a coroutine.
        """
        return await self.server.send(data, room=room, skip_sid=skip_sid,
                                      namespace=s_namespace or self.namespace,
                                      callback=callback)

    async def close_room(self, room, s_namespace=None):
        """Close a room.

        The only difference with the :func:`Server.close_room` method
        is that when the ``namespace`` argument is not given the namespace
        associated with the class is used.

        Note: this method is a coroutine.
        """
        return await self.server.close_room(
            room, namespace=s_namespace or self.namespace)

    async def get_session(self, sid, s_namespace=None):
        """Return the user session for a client.

        The only difference with the :func:`Server.get_session`
        method is that when the ``namespace`` argument is not given the
        namespace associated with the class is used.

        Note: this method is a coroutine.
        """
        return await self.server.get_session(
            sid, namespace=s_namespace or self.namespace)

    async def save_session(self, sid, session, s_namespace=None):
        """Store the user session for a client.

        The only difference with the :func:`Server.save_session`
        method is that when the ``namespace`` argument is not given the
        namespace associated with the class is used.

        Note: this method is a coroutine.
        """
        return await self.server.save_session(
            sid, session, namespace=s_namespace or self.namespace)

    def session(self, sid, s_namespace=None):
        """Return the user session for a client with context manager syntax.

        The only difference with the :func:`Server.session` method is
        that when the ``namespace`` argument is not given the namespace
        associated with the class is used.
        """
        return self.server.session(sid, namespace=s_namespace or self.namespace)

    async def disconnect(self, sid, s_namespace=None):
        """Disconnect a client.

        The only difference with the :func:`Server.disconnect` method
        is that when the ``namespace`` argument is not given the namespace
        associated with the class is used.

        Note: this method is a coroutine.
        """
        return await self.server.disconnect(
            sid, namespace=s_namespace or self.namespace)


class AsyncClientNamespace(namespace.ClientNamespace):
    """Base class for asyncio client-side class-based namespaces.

    A class-based namespace is a class that contains all the event handlers
    for a Socket.IO namespace. The event handlers are methods of the class
    with the prefix ``on_``, such as ``on_connect``, ``on_disconnect``,
    ``on_message``, ``on_json``, and so on. These can be regular functions or
    coroutines.

    :param namespace: The Socket.IO namespace to be used with all the event
                      handlers defined in this class. If this argument is
                      omitted, the default namespace is used.
    """

    def is_asyncio_based(self):
        return True

    async def trigger_event(self, event, *args):
        """Dispatch an event to the proper handler method.

        In the most common usage, this method is not overloaded by subclasses,
        as it performs the routing of events to methods. However, this
        method can be overriden if special dispatching rules are needed, or if
        having a single method that catches all events is desired.

        Note: this method is a coroutine.
        """
        handler_name = 'on_' + event
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            if asyncio.iscoroutinefunction(handler) is True:
                try:
                    ret = await handler(*args)
                except asyncio.CancelledError:  # pragma: no cover
                    ret = None
            else:
                ret = handler(*args)
            return ret

    async def emit(self, event, data=None, s_namespace=None, callback=None):
        """Emit a custom event to the server.

        The only difference with the :func:`Client.emit` method is
        that when the ``namespace`` argument is not given the namespace
        associated with the class is used.

        Note: this method is a coroutine.
        """
        return await self.client.emit(event, data=data,
                                      namespace=s_namespace or self.namespace,
                                      callback=callback)

    async def send(self, data, s_namespace=None, callback=None):
        """Send a message to the server.

        The only difference with the :func:`Client.send` method is
        that when the ``namespace`` argument is not given the namespace
        associated with the class is used.

        Note: this method is a coroutine.
        """
        return await self.client.send(data,
                                      namespace=s_namespace or self.namespace,
                                      callback=callback)

    async def disconnect(self):
        """Disconnect a client.

        The only difference with the :func:`Client.disconnect` method
        is that when the ``namespace`` argument is not given the namespace
        associated with the class is used.

        Note: this method is a coroutine.
        """
        return await self.client.disconnect()
