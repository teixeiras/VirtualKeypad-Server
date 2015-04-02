#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pipplware.web import sensors


def main():
    sensors.init()
    try:
        for chip in sensors.iter_detected_chips():
            print chip
            print 'Adapter:', chip.adapter_name
            for feature in chip:
                print '%s (%r): %.1f' % (
                    feature.name, feature.label, feature.get_value()
                )
                for subfeature in feature:
                    print '  %s: %.1f' % (
                        subfeature.name, subfeature.get_value()
                    )
            print
    finally:
        sensors.cleanup()


if __name__ == '__main__':
    main()
