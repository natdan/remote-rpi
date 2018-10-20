#################################################################################
# Copyright (c) 2018 Creative Sphere Limited.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License v2.0
# which accompanies this distribution, and is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#    Creative Sphere - initial API and implementation
#
#################################################################################


class PiCamera:

    def resolution(w, h):
        raise NotImplemented()

    def capture(self, camera, type, use_video_port=True):
        raise NotImplemented()

    def start_preview(self):
        raise NotImplemented()

    def stop_preview(self):
        raise NotImplemented()
