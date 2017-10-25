#! /usr/bin/env python3

# Core packages
import unittest

# Local packages
import app


class WebAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        self.app.application.config['VERSION_FILEPATH'] = 'fixtures/versions'
        self.app.application.template_folder = 'fixtures/templates'

    def _check_page(self, path, content, redirects=[], permanent_redirects=[]):
        """
        Test a list of paths all redirect to a specific destionation
        """

        for redirect in redirects:
            response = self.app.get(redirect)
            location = response.headers.get('Location')
            try:
                assert response.status_code == 302
                assert location == "http://localhost" + path
            except:
                import ipdb; ipdb.set_trace()
                pass

        for redirect in permanent_redirects:
            response = self.app.get(redirect)
            location = response.headers.get('Location')
            try:
                assert response.status_code == 301
                assert location == "http://localhost" + path
            except:
                import ipdb; ipdb.set_trace()
                pass

        response = self.app.get(path)
        try:
            assert response.status_code == 200
            assert response.data.decode('utf-8') == content
        except:
            import ipdb; ipdb.set_trace()
            pass

    def test_domain_root(self):
        response = self.app.get('/')
        location = response.headers.get('Location')
        assert response.status_code == 302
        assert location == "http://localhost/phone/"

    def test_homepage(self):
        self._check_page(
            path="/phone/en/",
            content="homepage",
            redirects=[
                '/phone',
                # '/phone/',
                # '/phone/en',
            ],
            permanent_redirects=[
                '/phone/en/index',
                '/phone/en/index.html',
            ]
        )
    #
    # def test_versioned_page(self):
    #     self._check_page(
    #         path="/phone/v1/versioned-page",
    #         content="versioned page v1",
    #         redirects=[
    #             '/phone/versioned-page',
    #             '/phone/versioned-page/',
    #             '/phone/v1/versioned-page/',
    #         ],
    #         permanent_redirects=[
    #             '/phone/v1/versioned-page/index',
    #             '/phone/v1/versioned-page/index.html',
    #         ]
    #     )
    #
    # def test_straight_up_file(self):
    #     self._check_page(
    #         path="/phone/straight-up",
    #         content="straight up page",
    #         redirects=['/phone/straight-up/'],
    #         permanent_redirects=[
    #             '/phone/straight-up.html',
    #             '/phone/straight-up/index',
    #             '/phone/straight-up/index.html',
    #         ]
    #     )
    #
    # def test_plain_directory(self):
    #     self._check_page(
    #         path="/phone/plain-directory/",
    #         content="plain directory",
    #         redirects=['/phone/plain-directory/'],
    #         permanent_redirects=[
    #             '/phone/plain-directory/index',
    #             '/phone/plain-directory/index.html',
    #         ]
    #     )
    #
    # def test_both(self):
    #     # Check directory version
    #     self._check_page(
    #         path="/phone/both/",
    #         content="dir",
    #         permanent_redirects=[
    #             '/phone/both/index',
    #             '/phone/both/index.html',
    #         ]
    #     )
    #     # Check file version
    #     self._check_page(
    #         path="/phone/both",
    #         content="file",
    #         permanent_redirects=['/phone/both.html']
    #     )
    #
    # def test_404s(self):
    #     non_urls = [
    #         '/both',
    #         '/phone/en/both',
    #         '/phone/en/versioned-page/',
    #         '/phone/v2/',
    #     ]
    #
    #     for path in non_urls:
    #         response = self.app.get(path)
    #         assert response.status_code == 404


if __name__ == '__main__':
    unittest.main()
