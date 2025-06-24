# Add contact URLs to the end of urlpatterns
urlpatterns += [
    # Contact URLs
    path('', include('portfolio_app.urls_contact')),
]