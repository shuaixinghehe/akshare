#! /usr/bin/env python
# *-* coding:utf-8 *-*
import web

urls = (
    '/check(.*)', 'Check'
)
app = web.application(urls, globals())


class Check:
    def GET(self, name):
        # data = web.input()

        return 'Hello, ' + name + '!'


if __name__ == "__main__":
    app.run()
