#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from functools import partial
from typing import Sequence

import cmk.gui.pages
import cmk.gui.plugins.metrics.graph_images as graph_images
import cmk.gui.plugins.metrics.html_render as html_render
from cmk.gui.metrics import page_graph_dashlet, page_host_service_graph_popup
from cmk.gui.plugins.metrics.utils import CombinedGraphMetricSpec
from cmk.gui.type_defs import CombinedGraphSpec


def resolve_combined_single_metric_spec(
    specification: CombinedGraphSpec,
) -> Sequence[CombinedGraphMetricSpec]:
    # Not available in CRE.
    return ()


def register_pages() -> None:
    for path, callback in (
        ("host_service_graph_popup", page_host_service_graph_popup),
        ("graph_dashlet", page_graph_dashlet),
        ("noauth:ajax_graph_images", graph_images.ajax_graph_images_for_notifications),
        ("ajax_graph", html_render.ajax_graph),
        ("ajax_render_graph_content", html_render.ajax_render_graph_content),
        ("ajax_graph_hover", html_render.ajax_graph_hover),
    ):
        cmk.gui.pages.register(path)(partial(callback, resolve_combined_single_metric_spec))


register_pages()
