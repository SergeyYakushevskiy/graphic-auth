package dstu.csae.auth.graphic.security;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class SameSiteCookieFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        chain.doFilter(request, response);

        if (response instanceof HttpServletResponse) {
            HttpServletResponse resp = (HttpServletResponse) response;
            // Получаем заголовки Set-Cookie, модифицируем их
            for (String header : resp.getHeaders("Set-Cookie")) {
                if (header.startsWith("jwt=") && !header.toLowerCase().contains("samesite")) {
                    String newHeader = header + "; SameSite=Strict";
                    resp.addHeader("Set-Cookie", newHeader);
                }
            }
        }
    }
}
