from django import template
from django.template.base import (FilterExpression, Node, TemplateSyntaxError,
                                  kwarg_re)
from django.utils.encoding import force_text

register = template.Library()


@register.tag
def query(parser, token):
    bits = token.split_contents()
    args = []
    asvar = None
    bits = bits[1:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                args.append({name: parser.compile_filter(value)})
            else:
                args.append(parser.compile_filter(value))

    return QueryNode(args, asvar)


class QueryNode(Node):
    def __init__(self, args, asvar):
        self.args = args
        self.asvar = asvar

    def render(self, context):
        def join(thing, lst):
            if isinstance(thing, dict):
                for k, v in thing.items():
                    if isinstance(v, FilterExpression):
                        v = force_text(v.resolve(context))
                    if v is None:
                        continue
                    lst.append('{}={}'.format(k, v))
            elif isinstance(thing, list):
                for it in thing:
                    if isinstance(it, FilterExpression):
                        it = it.resolve(context)
                    join(it, lst)
            elif isinstance(thing, str) and thing != '':
                lst.append(thing + '=')
            elif thing is None or thing == '':
                pass
            else:
                raise TypeError('Cannot join: %r' % thing)

        query_lst = []
        join(self.args, query_lst)
        query = '&'.join(query_lst)

        if self.asvar:
            context[self.asvar] = query
            return ''
        else:
            return query
