# Use the official Apache HTTP Server image
FROM httpd:2.4.69

# Copy your custom website files to the default Apache web root
COPY ./html/ /usr/local/apache2/htdocs/

# (Optional) Copy a custom Apache configuration file if you need one
# COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf

RUN find /usr/local/apache2/htdocs/ -type d -exec chmod 750 {} +
RUN find /usr/local/apache2/htdocs/ -type f -exec chmod 640 {} +
RUN chown -R www-data:www-data /usr/local/apache2/htdocs/

# Document that the container listens on port 80
EXPOSE 80
