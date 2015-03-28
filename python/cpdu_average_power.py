#!/usr/bin/env python
from gnuradio import gr
import json,time,os,pmt,numpy

class cpdu_average_power(gr.sync_block):
    def __init__(self, k=0):
        gr.sync_block.__init__(self, 
                name = "cpdu_average_power",
                in_sig = [],
                out_sig = []);
        self.k = k
        self.message_port_register_in(pmt.intern("cpdus"));
        self.message_port_register_out(pmt.intern("cpdus"));
        self.set_msg_handler(pmt.intern("cpdus"), self.handler);  

    def work(self, input_items, output_items):
        assert(False)

    def handler(self, pdu):
        data = pmt.to_python(pmt.cdr(pdu))
        meta = pmt.car(pdu)

        p = self.k + 10*numpy.log10(numpy.mean(numpy.real(data[0] * data[0])))
#        p = self.k + numpy.mean(data[0])
#        print data[0].shape,p

        meta = pmt.dict_add(meta, pmt.intern("power"), pmt.from_float( p ) )
        self.message_port_pub( pmt.intern("cpdus"), pmt.cons( meta, pmt.cdr(pdu) ) );
