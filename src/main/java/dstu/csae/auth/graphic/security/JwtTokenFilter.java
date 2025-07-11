package dstu.csae.auth.graphic.security;

import dstu.csae.auth.graphic.service.AccountService;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.JwtException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;
import org.springframework.util.AntPathMatcher;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Collections;

@Component
public class JwtTokenFilter extends OncePerRequestFilter {
    private JwtCore jwtCore;
    private AccountService accountService;

    @Autowired
    public JwtTokenFilter(JwtCore jwtCore, AccountService accountService) {
        this.jwtCore = jwtCore;
        this.accountService = accountService;
    }

    @Bean
    public String[] publicPaths() {
        return new String[] {
                "/login",
                "/login.html",
                "/register",
                "/register.html",
                "/api/**",
                "/css/**",
                "/js/**",
                "/img/**",
                "/json/**"
        };
    }

    private boolean isPublicPath(String path) {
        AntPathMatcher pathMatcher = new AntPathMatcher();
        for (String pattern : publicPaths()) {
            if (pathMatcher.match(pattern, path)) {
                return true;
            }
        }
        return false;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {

        String requestPath = request.getServletPath();

        if (isPublicPath(requestPath)) {
            filterChain.doFilter(request, response);
            return;
        }

        try {
            String jwt = null;
            // 1. Попытка получить JWT из cookie
            if (request.getCookies() != null) {
                for (var cookie : request.getCookies()) {
                    if ("jwt".equals(cookie.getName())) {
                        jwt = cookie.getValue();
                        break;
                    }
                }
            }

            // 2. Если из cookie не нашли, пробуем из заголовка Authorization
            if (jwt == null) {
                String headerAuth = request.getHeader("Authorization");
                if (headerAuth != null && headerAuth.startsWith("Bearer ")) {
                    jwt = headerAuth.substring(7);
                }
            }

            // 3. Обработка JWT, если найден
            if (jwt != null) {
                Claims claims;
                try {
                    claims = jwtCore.getClaims(jwt);
                } catch (ExpiredJwtException e) {
                    response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                    response.getWriter().write("JWT expired");
                    return;
                } catch (JwtException e) {
                    response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                    response.getWriter().write("Неверный JWT");
                    return;
                }

                String identifier = claims.getSubject();
                String purpose = claims.get("purpose", String.class); // может быть null

                if (identifier != null && SecurityContextHolder.getContext().getAuthentication() == null) {
                    UserDetails userDetails = accountService.loadByIdentifier(identifier);

                    if ("2fa".equals(purpose)) {
                        // Временный токен — разрешаем только доступ к /two-factor
                        if (!requestPath.startsWith("/two-factor")) {
                            response.sendRedirect("/two-factor");
                            return;
                        }

                        // Устанавливаем упрощённую аутентификацию (без authorities)
                        UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(
                                userDetails,
                                null,
                                Collections.emptyList()
                        );
                        SecurityContextHolder.getContext().setAuthentication(auth);

                    } else {
                        // Полноценный токен
                        UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(
                                userDetails,
                                null,
                                userDetails.getAuthorities()
                        );
                        SecurityContextHolder.getContext().setAuthentication(auth);
                    }
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        filterChain.doFilter(request, response);
    }

}
