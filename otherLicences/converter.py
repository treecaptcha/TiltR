import evdev
from evdev import ecodes, UInput
from collections import defaultdict


def toVirt(real, idx):

    # start of stolen from evdev
    '''
    Copyright (c) 2012-2016 Georgi Valkov. All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

      1. Redistributions of source code must retain the above copyright
         notice, this list of conditions and the following disclaimer.

      2. Redistributions in binary form must reproduce the above copyright
         notice, this list of conditions and the following disclaimer in
         the documentation and/or other materials provided with the
         distribution.

      3. Neither the name of author nor the names of its contributors may
         be used to endorse or promote products derived from this software
         without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    '''

    all_capabilities = defaultdict(set)

    filtered_types=(ecodes.EV_SYN, ecodes.EV_FF)

    for ev_type, ev_codes in real.capabilities().items():
        all_capabilities[ev_type].update(ev_codes)

    for evtype in filtered_types:
        if evtype in all_capabilities:
            del all_capabilities[evtype]


    caps: set = all_capabilities[3]

    caps.add((26, evdev.AbsInfo(value=128, min=0, max=255, fuzz=0, flat=15, resolution=0)))

    return UInput(name= "TiltR_" + str(idx), events=all_capabilities)
    # end of stolen from evdev
